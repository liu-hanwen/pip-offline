from pip._vendor import pkg_resources
import sys
import os

def argument_parse(args):
    if len(args)==1:
        raise ValueError('No argument available.')

    body = args[1:]
    args_dict = {}

    args_idxs = [idx for idx, value in enumerate(body) if value[0]=='-']

    if len(args_idxs)==1:
        args_dict[body[args_idxs[0]][1:]] = body[args_idxs[0]+1:]
        return args_dict
    
    for i in range(len(args_idxs)-1):
        start = args_idxs[i]
        end = args_idxs[i+1]
        if start+1==end:
            raise ValueError('Wrong format!')
        args_dict[body[start][1:]] = body[start+1:end]
    args_dict[body[end][1:]] = body[end+1:]
    return args_dict

def order_install(package, ret):
    if package in ret:
        return
        
    requirements = list(map(
        lambda x: str(x).replace('=','?').replace('>','?').replace('<','?').split('?', 1)[0].lower(),
        pkg_resources.working_set.by_key[package].requires()
    ))

    if len(requirements)==0:
        ret.append(package)
    else:
        for sub_package in requirements:
            order_install(sub_package, ret)
        ret.append(package)
        

def judge_if_format_correct(args):

    if 'i' not in args :
        raise ValueError('Please define what packages you want to install offline. "Example: -i flask numpy"')
    return True

def build_script(downloaded_list):
    template = "pip install ./packages/%s"
    return "set -e\n" + '\n'.join([template % package for package in downloaded_list]) + '\necho "DONE!"'
        

if __name__=='__main__':
    args = argument_parse(sys.argv)
    judge_if_format_correct(args)
    

    format_type = args['f'][0] if 'f' in args else 'zip'
    format_cmd_map = {
        'tar': 'tar -cvf %s %s',
        'tar.gz': 'tar -czvf %s %s',
        'tar.bz2': 'tar -cjvf %s %s',
        'zip': 'zip -r %s %s'
    }
    if format_type not in format_cmd_map:
        raise ValueError('Only [tar(default), tar.gz, tar.bz2, zip] are available.')
    format_cmd = format_cmd_map[format_type]

    output_name = args['n'][0] if 'n' in args else 'offline_installer'

    output_path = args['o'][0] if 'o' in args else './'
    if not os.path.exists(output_path):
        raise ValueError('Output path is not available.')

    os.system('mkdir ' + os.path.join(output_path, output_name))
    os.system('mkdir ' + os.path.join(output_path, output_name, 'packages'))
    install_list = []
    for package in args['i']:
        order_install(package, install_list)
    
    downloaded_list = []
    for package in install_list:
        before_files = set(os.listdir(os.path.join(output_path, output_name, 'packages')))
        os.system('pip download --no-binary :all: -d %s %s' % (os.path.join(output_path, output_name, 'packages'), package))
        after_files = set(os.listdir(os.path.join(output_path, output_name, 'packages')))
        new_file_name = list(after_files - before_files)[0]
        downloaded_list.append(new_file_name)
    
    with open(os.path.join(output_path, output_name, 'install.sh'), 'w') as f:
        f.write(build_script(downloaded_list))
    
    compress_cmd = format_cmd % (os.path.join(output_path, output_name+'.'+format_type), os.path.join(output_name, '*'))
    print(compress_cmd)
    cd_cmd = "cd %s" % output_path
    os.system(cd_cmd + '\n' + compress_cmd)

    delete_tmp_cmd = "rm -rf "+os.path.join(output_path, output_name)
    print(delete_tmp_cmd)
    os.system(delete_tmp_cmd)
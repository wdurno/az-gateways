from build.util import run
from time import sleep 

def deploy_service(root, conf): 
    'deploys service'
    interactive_debugging_mode = conf['interactive_debugging_mode']
    ## build image name  
    cmd1 = f'cat {root}/secret/acr/server' 
    acr_server = run(cmd1, return_stdout=True) 
    image_name = acr_server + '/' + conf['image_name']
    ## helm deploy 
    cmd2 = f'helm upgrade --install service {root}/src/helm/service '+\
            f'--set image={image_name} '
    run(cmd2, os_system=True) 
    pass



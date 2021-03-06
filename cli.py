import os 
import sys 
import yaml 
import argparse 

## args 
parser = argparse.ArgumentParser(description='Distributed Pytorch fitting with Horovod on Kubernetes.') 
parser.add_argument('--config-path', dest='config_path', type=str, default=None, help='path to config file') 
parser.add_argument('--no-docker-build', dest='no_docker_build', action='store_true', help='skip docker build step') 
parser.add_argument('--keep-docker-build-env', dest='keep_docker_build_env', action='store_true', default=False, \
        help='do not tear-down DinD after build, thereby retaining cached layers') 
parser.add_argument('--terraform-destroy', dest='terraform_destroy', action='store_true', help='tears-down everything') 
parser.add_argument('--terraform-destroy-compute', dest='terraform_destroy_compute', action='store_true', \
        help='destroys nodes, retains resource group and acr') 
parser.add_argument('--skip-terraform', dest='skip_terraform', action='store_true', help='skips all terraform build actions') 
parser.add_argument('--interactive-debugging-mode', dest='interactive_debugging_mode', action='store_true', \
        help='sleeps horovod pods for easier debugging')
args = parser.parse_args() 

## constants 
args.HOME = os.environ['HOME']  
args.ROOT = os.getcwd() 

## configure build env 
sys.path.append(os.path.join(args.ROOT, 'src', 'python')) 

## import build libs 
from build.terraform import guarantee_phase_1_architecture, guarantee_phase_2_architecture, terraform_destroy, \
        terraform_destroy_compute
from build.secret import refresh_keys 
from build.docker import docker_build 
from build.service import deploy_service 

## parse config path 
if args.config_path is None: 
    ## setting to default 
    config_path = os.path.join(args.HOME, 'az-gateways-config.yaml') 
    pass

## load config 
with open(config_path, 'r') as f: 
    args.config = yaml.safe_load(f) 
    args.config['interactive_debugging_mode'] = args.interactive_debugging_mode 
    pass

if args.terraform_destroy_compute:
    terraform_destroy_compute(args.ROOT, args.config) 
    exit(0) ## TODO need arg-checking logic. Will not terraform_destroy after this point. 
    pass 

if args.terraform_destroy: 
    terraform_destroy(args.ROOT, args.config) 
    exit(0) 
    pass

if not args.skip_terraform:
    ## deploy build-essential infrastructure 
    guarantee_phase_1_architecture(args.ROOT, args.config) 
    pass

## always refresh keys because tokens expire 
refresh_keys(args.ROOT, args.config) 

if not args.no_docker_build: 
    ## build service image 
    docker_build(args.ROOT, args.config, args.keep_docker_build_env) 
    pass

if not args.skip_terraform:
    ## deploy horovod compute infrastructure 
    guarantee_phase_2_architecture(args.ROOT, args.config) 
    pass 

deploy_service(args.ROOT, args.config)

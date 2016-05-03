#!/usr/bin/env python3

import subprocess
import re
import codecs

outfile = codecs.open('commands.md','w', 'utf-8')



# tests:
test=[]
test.append( u"Usage: juju sync-tools [options]\n\nSummary:\ncopy tools from the official tool store into a local model\n\nOptions:\n--all  (= false)\n    copy all versions, not just the latest\n--destination (= \"\")\n    local destination directory\n--dev  (= false)\n    consider development versions as well as released ones\n    DEPRECATED: use --stream instead\n--dry-run  (= false)\n    don't copy, just print what would be copied\n--local-dir (= \"\")\n    local destination directory\n-m, --model (= \"\")\n    Model to operate in\n--public  (= false)\n    tools are for a public cloud, so generate mirrors information\n--source (= \"\")\n    local source directory\n--stream (= \"\")\n    simplestreams stream for which to sync metadata\n--version (= \"\")\n    copy a specific major[.minor] version\n\nDetails:\nThis copies the Juju tools tarball from the official tools store (located\nat https://streams.canonical.com/juju) into your model.\nThis is generally done when you want Juju to be able to run without having to\naccess the Internet. Alternatively you can specify a local directory as source.\n\nSometimes this is because the model does not have public access,\nand sometimes you just want to avoid having to access data outside of\nthe local cloud.\n")
test.append( u"Usage: juju bootstrap [options] <controller name> <cloud name>[/region]\n\nSummary:\nInitializes a cloud environment.\n\nOptions:\n--agent-version (= \"\")\n    Version of tools to use for Juju agents\n--auto-upgrade  (= false)\n    Upgrade to the latest patch release tools on first bootstrap\n--bootstrap-constraints  (= )\n    Specify bootstrap machine constraints\n--bootstrap-series (= \"\")\n    Specify the series of the bootstrap machine\n--config  (= )\n    Specify a controller configuration file, or one or more configuration\n    options\n    (--config config.yaml [--config key=value ...])\n--constraints  (= )\n    Set model constraints\n--credential (= \"\")\n    Credentials to use when bootstrapping\n-d, --default-model (= \"default\")\n    Name of the default hosted model for the controller\n--keep-broken  (= false)\n    Do not destroy the model if bootstrap fails\n--metadata-source (= \"\")\n    Local path to use as tools and/or metadata source\n--no-gui  (= false)\n    Do not install the Juju GUI in the controller when bootstrapping\n--to (= \"\")\n    Placement directive indicating an instance to bootstrap\n--upload-tools  (= false)\n    Upload local version of tools before bootstrapping\n\nDetails:\nInitialization consists of creating an 'admin' model and provisioning a\nmachine to act as controller.\nCredentials are set beforehand and are distinct from any other\nconfiguration (see `juju add-credential`).\nThe 'admin' model typically does not run workloads. It should remain\npristine to run and manage Juju's own infrastructure for the corresponding\ncloud. Additional (hosted) models should be created with `juju create-\nmodel` for workload purposes.\nNote that a 'default' model is also created and becomes the current model\nof the environment once the command completes. It can be discarded if\nother models are created.\nIf '--bootstrap-constraints' is used, its values will also apply to any\nfuture controllers provisioned for high availability (HA).\nIf '--constraints' is used, its values will be set as the default\nconstraints for all future workload machines in the model, exactly as if\nthe constraints were set with `juju set-model-constraints`.\nIt is possible to override constraints and the automatic machine selection\nalgorithm by assigning a \"placement directive\" via the '--to' option. This\ndictates what machine to use for the controller. This would typically be\nused with the MAAS provider ('--to <host>.maas').\nYou can change the default timeout and retry delays used during the\nbootstrap by changing the following settings in your configuration file\n(all values represent number of seconds):\n    # How long to wait for a connection to the controller\n    bootstrap-timeout: 600 # default: 10 minutes\n    # How long to wait between connection attempts to a controller\naddress.\n    bootstrap-retry-delay: 5 # default: 5 seconds\n    # How often to refresh controller addresses from the API server.\n    bootstrap-addresses-delay: 10 # default: 10 seconds\nPrivate clouds may need to specify their own custom image metadata and\ntools/agent. Use '--metadata-source' whose value is a local directory.\nThe value of '--agent-version' will become the default tools version to\nuse in all models for this controller. The full binary version is accepted\n(e.g.: 2.0.1-xenial-amd64) but only the numeric version (e.g.: 2.0.1) is\nused. Otherwise, by default, the version used is that of the client.\n\nExamples:\n    juju bootstrap mycontroller google\n    juju bootstrap --config=~/config-rs.yaml mycontroller rackspace\n    juju bootstrap --config agent-version=1.25.3 mycontroller aws\n    juju bootstrap --config bootstrap-timeout=1200 mycontroller azure\n\nSee also:\n    add-credentials\n    create-model\n    set-constraints")

# useful text
pad='   '
pagetext=("Title:Juju commands and usage\n\n"
          "# Juju Command reference\n\n"
          "You can get a list of the currently used commands by entering\n" 
          "```juju help commands``` from the commandline. The currently"
          " understood commands\nare listed here, with usage and examples.\n\n"
          "Click on the expander to see details for each command. \n\n")

commands = subprocess.check_output(['juju', 'help', 'commands']).splitlines()
outfile.write(pagetext)
for c in commands:
    print(c)
    header = '^# '+str(c.split()[0])+ '\n\n'
    htext = subprocess.check_output(['juju', 'help', c.split()[0].decode('unicode_escape')])
    p = re.compile(u'Usage:(.+?)\n\nSummary:\n(.+?)\n\nOptions:\n(.+?)Details:\n(.+)', re.DOTALL)
    h=re.findall(p, htext.decode('unicode_escape'))
    if not h:
      print("**SEVERE WARNING**: {} has no DETAILS!".format(c.split()[0]))
      p = re.compile(u'Usage:(.+?)\n\nSummary:\n(.+?)\n\nOptions:\n(.+?)', re.DOTALL)
      h=re.findall(p, htext.decode('unicode_escape'))
      help=(h[0][0],h[0][1],h[0][2],"Details:\nNo further information.")
    else:
      help=h[0]
    usage=pad+"**Usage:** `"+help[0]+"`\n\n"
    summary=pad+"**Summary:**\n\n"+pad+help[1]+"\n\n"
    options = pad+'**Options:**\n\n'
    option_lines = help[2].split('\n')

    for line in option_lines:
       if (line !=''):
          if (line[0]=='-'):
             options = options+pad+"_"+line.strip()+"_\n\n"
          else:
             options = options+pad+pad+line.strip()+"\n\n"

    details=help[3]
    examples=''
    also=''
    alias=''

    # search for Aliases section
    # if it exists, truncate details and process
    q= re.compile(u'Aliases: ?(.+?)$',re.DOTALL | re.IGNORECASE)
    x = re.search( q, details)
    if x:
      print('match')
      match=details[x.start()+8:].split(' ')
      details=details[:x.start()] # truncate the bit we matched
      alias=pad+'**Aliases:**\n\n'
      
      for line in match:
        if (line !=''):
          alias = alias+pad+pad+'`'+line.strip()+'`\n\n'    




    # search for see also section
    # if it exists, truncate details and process
    q= re.compile(u'See also: ?\n(.+?)$',re.DOTALL | re.IGNORECASE)
    x = re.search( q, details)
    if x:
      match=details[x.start()+11:].split('\n')
      details=details[:x.start()] # truncate the bit we matched
      also=pad+'**See also:**\n\n'
      
      for line in match:
        if (line !=''):
          also = also+pad+pad+'`'+line.strip()+'`\n\n'

    # search for Examples section
    # if it exists, truncate details and process
    q= re.compile(u'Examples:\n(.+?)$',re.DOTALL)
    x = re.search( q, details)
    if x:
      match=details[x.start()+10:].split('\n')
      details=details[:x.start()] # truncate the bit we matched
      examples=pad+'**Examples:**\n\n'
      
      for line in match:
        if (line !=''):
          if (line[0]==' '):
            examples=examples+pad
            pass
          examples = examples+pad+line+'\n'
      examples += '\n\n'
    else:
      print("WARNING: {} has no examples!".format(c.split()[0]))
    #process the rest of details section.
    section=''
    iflag=False
    for line in details.split('\n'):
       if (line !=''):
          if (line[0]==' '):
             line= pad+pad+line
             iflag=True
          elif iflag:
             line= '\n'+pad+line
             print(line)
             iflag=False
          if ((len(line)<70) & ((line[-1:]=='.') | (line[-1:]==':'))):
             line=line+'\n'
          section = section+'\n'+pad +line
    details= '\n   **Details:**\n\n'+section+'\n\n'
    outfile.write(header+usage+summary+options+details+examples+also+alias+'\n\n')

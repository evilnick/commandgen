#!/usr/bin/env python3

import subprocess
import re

outfile = open('commands.md','w')



# tests:
test=[]
test.append( u"Usage: juju sync-tools [options]\n\nSummary:\ncopy tools from the official tool store into a local model\n\nOptions:\n--all  (= false)\n    copy all versions, not just the latest\n--destination (= \"\")\n    local destination directory\n--dev  (= false)\n    consider development versions as well as released ones\n    DEPRECATED: use --stream instead\n--dry-run  (= false)\n    don't copy, just print what would be copied\n--local-dir (= \"\")\n    local destination directory\n-m, --model (= \"\")\n    Model to operate in\n--public  (= false)\n    tools are for a public cloud, so generate mirrors information\n--source (= \"\")\n    local source directory\n--stream (= \"\")\n    simplestreams stream for which to sync metadata\n--version (= \"\")\n    copy a specific major[.minor] version\n\nDetails:\nThis copies the Juju tools tarball from the official tools store (located\nat https://streams.canonical.com/juju) into your model.\nThis is generally done when you want Juju to be able to run without having to\naccess the Internet. Alternatively you can specify a local directory as source.\n\nSometimes this is because the model does not have public access,\nand sometimes you just want to avoid having to access data outside of\nthe local cloud.\n")

pad='   '

# c = subprocess.check_output(['juju', 'help', 'commands']).splitlines()
# for command in c:

for t in test:
    p = re.compile(u'Usage:(.+?)\n\nSummary:\n(.+?)\n\nOptions:\n(.+?)Details:\n(.+)', re.DOTALL)
    #p = re.compile(ur'Usage:(.+?)\n\nSummary:\n(.+?)\n\nOptions:\n(.+?)Details:\n(.+)', re.DOTALL)
    #test_str = u"Usage: juju sync-tools [options]\n\nSummary:\ncopy tools from the official tool store into a local model\n\nOptions:\n--all  (= false)\n    copy all versions, not just the latest\n--destination (= \"\")\n    local destination directory\n--dev  (= false)\n    consider development versions as well as released ones\n    DEPRECATED: use --stream instead\n--dry-run  (= false)\n    don't copy, just print what would be copied\n--local-dir (= \"\")\n    local destination directory\n-m, --model (= \"\")\n    Model to operate in\n--public  (= false)\n    tools are for a public cloud, so generate mirrors information\n--source (= \"\")\n    local source directory\n--stream (= \"\")\n    simplestreams stream for which to sync metadata\n--version (= \"\")\n    copy a specific major[.minor] version\n\nDetails:\nThis copies the Juju tools tarball from the official tools store (located\nat https://streams.canonical.com/juju) into your model.\nThis is generally done when you want Juju to be able to run without having to\naccess the Internet. Alternatively you can specify a local directory as source.\n\nSometimes this is because the model does not have public access,\nand sometimes you just want to avoid having to access data outside of\nthe local cloud.\n"
     
    help=re.findall(p, t)[0]
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
    outfile.write(usage+summary+options)

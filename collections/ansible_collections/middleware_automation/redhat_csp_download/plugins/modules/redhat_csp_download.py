#!/usr/bin/python

# Written By - Andrew Block <andy.block@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
##############################################################################

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: redhat_csp_download
author: Andrew Block (@sabre1041)
version_added: "1.2.0"
short_description: Downloads resources from the Red Hat customer portal.
description:
    - Downloads resources from the Red Hat customer portal.
requirements:
    - requests
    - lxml
extends_documentation_fragment:
    - files
options:
    username:
        description:
            - Red Hat Customer Portal username.
        type: str
        required: true
    password:
        description:
            - Red Hat Customer Portal username.
        type: str
        required: true
    url:
        description:
            - Protected Red Hat Customer Portal resource.
        type: str
        required: true
    dest:
        description:
            - absolute path of where to download the file to.
        type: str
        required: true
'''


EXAMPLES = '''
- name: Download JBoss EAP Zip
  redhat_csp_download:
    username=foo@example.com
    password=bar
    url=https://access.redhat.com/jbossnetwork/restricted/softwareDownload.html?softwareId=37193
    dest=/tmp/eap-connectors.zip
'''


try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import lxml.html
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


def get_csp_file(module, username, password, url, dest):

    # Setup Auth Struct
    auth = {'username': username, 'password': password}

    session = requests.Session()

    # Get initial request
    r = session.get(url)

    # Parse initial response
    root = lxml.html.fromstring(r.text)

    post_url = root.xpath('//form[@method="post"]')[0].action

    data = {'username': username, 'password': password}

    # Final Post to download file
    r = session.post(post_url, data=data)

    # Check if html page is returned indicating failure
    if 'html' not in r.headers['Content-Type']:

        # Download file
        with open(dest, "wb") as code:
            code.write(r.content)
    else:
        module.fail_json(msg="An error occurred retrieving content")

    # Close session
    session.close()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            username=dict(required=True),
            password=dict(no_log=False, required=True),
            url=dict(required=True),
            dest=dict(required=True)
        ),
        add_file_common_args=True
    )

    if not HAS_REQUESTS:
        module.fail_json(msg='requests is required for this module')

    if not HAS_LXML:
        module.fail_json(msg='lxml is required for this module')

    username = module.params.get('username')
    password = module.params.get('password')
    url = module.params.get('url')
    dest = module.params.get('dest')

    if os.path.exists(dest):
        # allow file attribute changes
        module.params['path'] = dest
        file_args = module.load_file_common_arguments(module.params)
        file_args['path'] = dest
        changed = module.set_fs_attributes_if_different(file_args, False)

        if changed:
            module.exit_json(msg="file already exists but file attributes changed", dest=dest, url=url, changed=changed)
        module.exit_json(msg="file already exists", dest=dest, url=url, changed=changed)

    try:
        get_csp_file(module, username, password, url, dest)
    except Exception as ex:
        module.fail_json(msg=str(ex))

    changed = True

    res_args = dict(
        url=url, dest=dest, changed=changed, msg="OK"
    )

    module.exit_json(**res_args)


from ansible.module_utils.basic import AnsibleModule, os
if __name__ == '__main__':
    main()

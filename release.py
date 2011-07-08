import os
import sys
import re
import optparse

''' TODO:
  Need to add in logging to std out - just something simple
  need to throw when things go off in active functions
  need to compile and make sure it all works.  THis is going to be hard to test
  '''
class ReleaseOptions(optparse.OptionParser):
    def __init__(self, **kwargs):
        optparse.OptionParser.__init__(self, **kwargs)
        defaults = {}

        # Add the options here
        self.add_option("--git-uri",
                        action = "store", type = "string", dest = "git_uri",
                        help = "Git URI to check out mozmill from")
        defaults["git_uri"] = None
        
        self.add_option("--branch",
                        action = "store", type = "string", dest = "branch",
                        help = "Git branch to checkout and release - must be branch name, defaults to master")
        defaults["branch"] = master

        self.add_option("--version-diff",
                        action = "store", type = "string", dest = "version_diff",
                        help = "Diff file to use for updating versions")
        defaults["version_diff"] = None

        self.add_option("--push_to_pypi",
                        action = "store_true", dest = "push_to_pypi",
                        help = "Whether or not to push to pypi, defaults to false")
        defaults["push_to_pypi"] = False

        # Set the defaults
        self.set_defaults(**defaults)

    def verify_options(self, options):
        if options.version_diff:
            if not os.path.exists(options.version_diff):
                print "ERROR: Version diff: %s does not exist" % options.version_diff
                sys.exit(1)
        
        if not options.get_uri:
            print "ERROR: You must specify a git URI to check out the mozmill source!"
            sys.exit(1)
        
def checkout_mozmill(url, branch):
    if branch == "master":
        p = subprocess.Popen(["git", "clone", url], stdout = subprocess.PIPE, shell=True)
        output = p.communicate()[0]
        if p.returncode != 0:
           print "ERROR during git clone: (original output to follow):"
           print output
           sys.exit(1)


def main():
    # Parse your opts
    parser = ReleaseOptions()
    options, args = parser.parse_args()
    parser.verify_options(options)

    # Get the code
    checkout_mozmill(options.git_uri, options.branch)

    # Update it if needed
    if options.version_diff:
        update_versions(options.version_diff)

    # Now push to pypi
    if options.push_to_pypi:
        push_to_pypi()
    else:
        # Then we upload to a place where we stage the bits
        # do this via curl?
        print "Pushing to a non-pypi server is not implemented yet"

if __name__ == '__main__':
    main()

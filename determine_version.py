from subprocess import Popen, PIPE
import re

DELIMITERS=["."]

def split(tag):
    regex=re.compile("(^.*[%s]{0,1})(\d+)"% ''.join(DELIMITERS))
    assert regex.match(tag)
    return regex.match(tag).group(1), int(regex.match(tag).group(2))

def next(tag):
    prefix, number=split(tag)
    return prefix+str(number+1)

# the prefix includes the separator
def get_last_tag(prefix):
    p = Popen(['git', 'ls-remote', 'origin'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    last="%s0"%prefix
    output, err = p.communicate()
    p=re.compile("^.*refs/tags/(%s\d+)$"%prefix)
    for line in [s.strip() for s in output.splitlines()]:
        print line
        if p.match(line):
            tag=p.match(line).group(1)
            if split(tag)[1]>split(last)[1]:
                last=tag
    return last


release_branch_regex=re.compile("^.*release/(\d+\.\d+)$")
feature_branch_regex=re.compile("^.*feature/.*-(\d+)$")

def get_next_version(branch):
    result=":-)"
    if "develop"==branch:
        return next(get_last_tag("0.0."))
    elif release_branch_regex.match(branch):
        first_part=release_branch_regex.match(branch).group(1)
        return next(get_last_tag(first_part+"."))
    elif feature_branch_regex.match(branch):
        feature_number=feature_branch_regex.match(branch).group(1)
        return next(get_last_tag("0."+feature_number+"."))
    else:
        return None


def main():
    print "Determining version which is going to be built"
    branch=None
    branch_numer=None
    p = Popen(['git', 'branch'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    p=re.compile("^\* (.*)")
    for line in [s.strip() for s in output.splitlines()]:
        if p.match(line):
            branch = p.match(line).group(1)
            print "branch is %s" % branch
    print "next version should be %s" % get_next_version(branch)


if __name__ == "__main__":
    main()

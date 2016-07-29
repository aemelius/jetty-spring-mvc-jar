from subprocess import Popen, PIPE
import re


def split(tag, prefix):
    regex=re.compile("(%s)(\d+)"% prefix)
    assert regex.match(tag)
    return regex.match(tag).group(1), int(regex.match(tag).group(2))

def next(tag, prefix):
    prefix, number=split(tag, prefix)
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
            if split(tag, prefix)[1]>split(last, prefix)[1]:
                last=tag
    return last


release_branch_regex=re.compile("^.*release/(\d+\.\d+)$")
feature_branch_regex=re.compile("^.*feature/.*-(\d+)$")

def get_next_version(branch):
    result=":-)"
    if "develop"==branch:
        prefix="0.0."
        return next(get_last_tag(prefix), prefix)
    elif release_branch_regex.match(branch):
        first_part=release_branch_regex.match(branch).group(1)
        prefix=first_part+"."
        return next(get_last_tag(prefix), prefix)
    elif feature_branch_regex.match(branch):
        feature_number=feature_branch_regex.match(branch).group(1)
        prefix =  "0.%s."%feature_number
        return next(get_last_tag(prefix), prefix)
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

from subprocess import Popen, PIPE
import re


def split(label):
    regex=re.compile("(.*)(\d+)")
    assert regex.match(label)
    return regex.match(label).group(1), int(regex.match(label).group(2))

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

def get_develop_prefix():
    p = Popen(['git', 'ls-remote', 'origin'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    last_major=0
    last_minor=0
    output, err = p.communicate()
    p=re.compile("^.*refs/heads/release/(\d+)\.(\d+)$")
    for line in [s.strip() for s in output.splitlines()]:
        print line
        if p.match(line):
            major=p.match(line).group(1)
            minor=p.match(line).group(2)

            if major>=last_major:
                last_major=major
                if minor>last_minor:
                    last_minor=minor
                    
    return "%s.%s"% (last_major, last_minor)

release_branch_regex=re.compile("^.*release/(\d+\.\d+)$")
feature_branch_regex=re.compile("^.*feature/.*-(\d+)$")

def get_next_version(branch):
    result=":-)"
    if "develop"==branch:
        prefix=get_develop_prefix()+"."
        print prefix
        return next(get_last_tag(prefix))
    elif release_branch_regex.match(branch):
        first_part=release_branch_regex.match(branch).group(1)
        prefix=first_part+"."
        return next(get_last_tag(prefix))
    elif feature_branch_regex.match(branch):
        feature_number=feature_branch_regex.match(branch).group(1)
        prefix =  "0.%s."%feature_number
        return next(get_last_tag(prefix))
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

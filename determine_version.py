from subprocess import Popen, PIPE
import re

def split(tag):
    regex=re.compile("(^.*[-.])(\d+)")
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


#assert get_last_tag("v1.0.")=="v1.0.0"
#last_tag=get_last_tag("8.0.8.")
#assert last_tag=="8.0.8.0", "last tag is not %s !" % "8.0.8.0" 


#assert next(get_last_tag("8.0.8."))=="8.0.8.1"
#assert next(get_last_tag("8.0."))=="8.0.9"

assert next("abcd-1234")=="abcd-1235"
assert next("abcd.1")=="abcd.2"
assert next("abcd-12")=="abcd-13"
assert next("abcd-0")=="abcd-1"

release_branch_regex=re.compile("^.*release/(\d+\.\d+)$")
feature_branch_regex=re.compile("^.*feature/.*-(\d+)$")

def get_next_version(branch):
    result=":-)"
    if "develop"==branch:
        #prefix, previous_sprint=splitdd(get_last_tag("END_OF_SPRINT-"))
        return next(get_last_tag("d."))
    elif release_branch_regex.match(branch):
        first_part=release_branch_regex.match(branch).group(1)
        return next(get_last_tag("r"+first_part+"."))
    elif feature_branch_regex.match(branch):
        first_part=feature_branch_regex.match(branch).group(1)
        return next(get_last_tag("f"+first_part+"."))
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

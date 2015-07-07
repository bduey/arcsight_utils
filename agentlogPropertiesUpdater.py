import re
import sys
import datetime
from shutil import move

# set appopriate field values
fieldsToReplace = {
    'followexternalrotation': 'true',
    'usealternaterotationdetection': 'false',
    'wildcard': 'agent.log',
    'extractregex': '.*/(.*)/current/logs/.*',
    'extractsource': 'File Path',
    'usefieldextractor': 'true',
    'extractfieldnames': 'filePath',
    'startatend': 'true'
}

# read command line input for file name
try:
    propertyFile = sys.argv[1]
except IndexError:
    print "No file specified. Syntax: agentlogPropertiesUpdater.py /path/to/file/agent.properties"
    sys.exit(0)

# Make backup of existing properties file 
todayString = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
backupFileName = '%s.%s' % (propertyFile, todayString)
move(propertyFile, backupFileName)

# open files
propertyFileWriteObject = open(propertyFile, 'w')
propertyFileReadObject = open(backupFileName, 'r')

for line in propertyFileReadObject:
    outLine = ''
    # for each line, parse with a regex string
    match = re.search("^agents\[\d\]\.foldertable\[(?P<tableNum>\d+)\]\.(?P<field>\w+)=(?P<value>.+|)$", line)

    if match:
        if match.group('field') in fieldsToReplace and match.group('value') != fieldsToReplace[match.group('field')]:
            outLine = str.replace(line, '=%s' % match.group('value'), '=%s' % fieldsToReplace[match.group('field')])
            print "For foldertable %s and field %s, replaced %s with %s." % (
                match.group('tableNum'),
                match.group('field'), 
                match.group('value'), 
                fieldsToReplace[match.group('field')])
    
    # write out new line if changed
    if outLine:
        propertyFileWriteObject.write(outLine)
    else:
        propertyFileWriteObject.write(line)

propertyFileReadObject.close()
propertyFileWriteObject.close()
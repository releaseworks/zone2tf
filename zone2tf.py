import sys


def _gen_zone(**d):
    return '''
resource "aws_route53_zone" "{root_zone_name}" {{
  name = "{root_zone}"
}}'''.format(**d)

def _gen_record(**d):
    return '''
resource "aws_route53_record" "{record_name}" {{
  zone_id = "${{aws_route53_zone.{root_zone_name}.id}}"
  name    = "{name}"
  type    = "{type}"
  records = ["{record}"]
  ttl     = {ttl}
}}'''.format(**d)

if len(sys.argv) < 2:
    print "Usage:\n{0} <zonefile>".format(sys.argv[0])
    exit(1)

with open(sys.argv[1], 'r') as zone_file:
    root_zone = ''
    root_zone_name = ''

    for line in zone_file:

        # skip line if it's not a record
        if ' IN ' not in line:
            continue
        
        parts = line.split(' ')

        # try and find the root zone
        if parts[2] == 'SOA':
            root_zone = parts[0]
            root_zone_name = root_zone.replace('.','')

            print _gen_zone(root_zone=root_zone,
                            root_zone_name=root_zone_name)
            continue
        
        record_type = parts[3]

        # remove newline and white characters from record
        # and expand to include the rest of line if type can include spaces
        if record_type in ('MX', 'SRV', 'TXT'):
            record = ' '.join(parts[4:]).strip()
        else:
            record = parts[4].strip()

        # strip the root zone from the end of the string
        if parts[0].endswith('.{0}.'.format(root_zone)):
            record_name = parts[0][:-(len(root_zone) + 2)]
        else:
            record_name = parts[0]

        # strip double quotes if type is txt
        if record_type == 'TXT' and parts[4].startswith('"'):
            record = record[1:-1]

        record_ttl = int(parts[1])

        print _gen_record(record_name='{0}-{1}'.format(parts[0].replace('.',''),parts[3].lower()),
                          name=record_name,
                          ttl=record_ttl,
                          type=record_type,
                          record=record,
                          root_zone_name=root_zone_name)

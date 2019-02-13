# zone2tf
A script to convert a Bind-compatible DNS zone file to Terraform AWS Route53 configuration.

This script is quick, dirty and will not handle all use cases. Use it as a starting point.

## Usage
```
$ git clone https://github.com/releaseworks/zone2tf.git
$ cd zone2tf/
$ python zone2tf.py my_zone.txt

resource "aws_route53_zone" "myzone-com" {
  name = "myzone.com"
}

resource "aws_route53_record" "wwwmyzonecom-a" {
  zone_id = "${aws_route53_zone.myzone-com.id}"
  name    = "www"
  type    = "A"
  records = ["127.0.0.1"]
  ttl     = 3600
}
...
```

To redirect to a file:
```
python zone2tf.py my_zone.txt > route53.tf
```


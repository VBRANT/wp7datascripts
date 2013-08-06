'''Sample Python code to invoke GNRD name doiscovery service.

Two sample files are provided: call_gnrd_sample.txt and
call_gnrd_sample_big.txt. The expected results are shown in
call_gnrd_sample_results.json and call_gnrd_sample_big_results.json
respectively.

David King <David.King@open.ac.uk>
for ViBRANT <http://vbrant.eu//>
August 2013

License: GPLv2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt>
'''

import json
from time import sleep
from urllib import request, parse

def call_gnrd(service_url, source_file):
    with open(source_file, 'r', encoding='utf-8') as f:
        text_to_parse = f.read()
    parms = {
    'text' : text_to_parse
    }
    querystring = parse.urlencode(parms)
    response = request.urlopen(service_url+'?' + querystring)
    json_resp = response.read()
    resp = json.loads(json_resp.decode('utf-8'))
    if resp['status'] == 303:
        print('Request being processed')
        next_req = resp['token_url']
        sleep(5)
        response = request.urlopen(next_req)
        json_resp = response.read()
        resp = json.loads(json_resp.decode('utf-8'))
        results_file = source_file.replace('txt', 'json')
        with open(results_file, 'w', encoding='utf-8') as f:
            f.write(str(resp))
            print('Request completed\nResults written to {}'.format(results_file))
    else:
        print('Problem with request\n{}'.format(str(resp)))

if __name__ == '__main__':
    call_gnrd('http://gnrd.oerc.ox.ac.uk/name_finder.json',
              'call_gnrd_sample.txt')
              # 'call_gnrd_sample_big.txt')
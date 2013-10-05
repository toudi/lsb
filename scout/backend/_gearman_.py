import gearman
from ConfigParser import SafeConfigParser
import json

config = SafeConfigParser()
config.read('conf/scout.conf')

class JSONDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)

class JSONGearmanClent(gearman.GearmanClient):
    data_encoder = JSONDataEncoder

class Backend(object):
    def submit(self, job):
        client = JSONGearmanClent(config.get('gearman', 'hosts').split(','))
        return client.submit_job(
            ('%s.%s' % (job.pop('worker'), job.pop('method'))).encode('utf-8'),
            job,
            background=True
        )
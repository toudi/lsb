import json # Or similarly styled library
from ConfigParser import SafeConfigParser
import gearman

config = SafeConfigParser()
config.read('conf/scout.conf')

class JSONDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)

class JSONWorker(gearman.GearmanWorker):
    data_encoder = JSONDataEncoder


def hello_world(worker, job):
    print("got a job to do!", job)
    return True

worker = JSONWorker(config.get('gearman', 'hosts').split(','))
worker.register_task('foo.bar.helloworld', hello_world)
worker.work()
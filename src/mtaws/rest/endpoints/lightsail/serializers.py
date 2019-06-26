from flask_restplus import fields
from mtaws.rest.api import api
from mtaws.rest.endpoints.serializers import (
    paginated, account
)

lightsail_instance = api.model('lightsail_instance', {
    'id': fields.String(readonly=True,  description='Lightsail primary key UUID'),
    'created': fields.DateTime(readonly=True,  description='UTC DateTime of instance creation'),
    'instance_name': fields.String(description='Name Tag of the instance'),
    'instance_id': fields.String(readonly=True,  description='AWS EC2 Instance ID'),
    'instance_type': fields.String(readonly=True, description='EC2 Instance type'),
    'eip_v4': fields.String(readonly=True,  description='IPV4 Public IP'),
    'eip_allocation_id': fields.String(readonly=True,  description='EIP Allocation ID')
})

lightsail_instance_list = api.inherit('lightsail_instance_list', paginated, {
    'lightsail_instances': fields.List(fields.Nested(lightsail_instance)),
    'account': fields.Nested(account)

})

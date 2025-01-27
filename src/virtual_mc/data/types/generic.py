
'''
Generic definition of object which can be transmitted over the TCP connection
'''

class Byteable_Object:
    
    def to_bytes(self):
        raise NotImplementedError('This functionality is not implemented on this object type!')
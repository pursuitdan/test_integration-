import multiprocessing as mp

class SyncManager:

     def __init__(self):
          super(SyncManager, self).__init__() #inherit from the object class
          self.mgr = mp.Manager() #the mem manager allows for access from multiple processes
          self.count = self.mgr.Value('i',0)
          self.last_id = self.mgr.Value('i',0)
          self.lock = mp.Lock() # use locks to support shared access since list is not locked by default
     
     # called by the stream processor when it is done streaming
     def stop(self,last_id): 
          with self.lock:
               self.count.value = 1
               self.count.last_id = last_id

     # called by the db analytics when it wants to know the last search value. 
     def get_last_id(self):
         return self.last_id 

     # returns true if the signal is still streaming
     def sending(self):
          return (self.count.value == 0)
               


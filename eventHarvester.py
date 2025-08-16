import pygame, threading


class eventHarvester:
    def __init__(self):
        self.eventQueue = []
        self.lock = threading.Lock()
        self.tempQueue = []
        self.continuing = True
        threading.Thread(target=self.__harvestEvents, daemon=True).start()

    def __harvestEvents(self):
        pygame.display.set_mode()
        while self.continuing:
            if len(self.tempQueue) > 0:
                if self.lock.acquire(blocking=False):
                    for e in self.tempQueue:
                        self.eventQueue.append(e)
                    self.lock.release()
                    self.tempQueue.clear()
                else:
                    potentialEvent = pygame.event.wait(1)
                    if potentialEvent.type != pygame.NOEVENT:
                        potentialEvent.time = pygame.time.get_ticks()
                        self.tempQueue.append(potentialEvent)
            else:
                nextEvent = pygame.event.wait(10)
                if nextEvent.type != pygame.NOEVENT:
                    nextEvent.time = pygame.time.get_ticks()
                    self.tempQueue.append(nextEvent)

    def getEvents(self) -> list:
        response = []
        if self.lock.acquire(blocking=False):
            for e in self.eventQueue:
                response.append(e)
            self.eventQueue.clear()
            self.lock.release()
        return response

    def stop(self):
        self.continuing = False
        
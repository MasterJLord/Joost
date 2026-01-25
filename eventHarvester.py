import pygame, threading


class eventHarvester:
    def __init__(self, dontstartrunning : False):
        self.eventQueue = []
        self.lock : threading.Lock = threading.Lock()
        self.captionLock = threading.Lock()
        self.tempQueue = []
        self.continuing = True
        self.recaptionNeeded = False
        self.caption = "Joost"
        if not dontstartrunning:
            threading.Thread(target=self.harvestEvents, daemon=True).start()

    def harvestEvents(self):
        try:
            pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h - 75), pygame.RESIZABLE)
            pygame.display.set_caption(self.caption)
            while self.continuing:
                if len(self.tempQueue) > 0:
                    if self.lock.acquire():
                        for e in self.tempQueue:
                            if e.type == pygame.VIDEORESIZE:
                                print("received")
                            self.eventQueue.append(e)
                        self.lock.release()
                        self.tempQueue.clear()
                    else:
                        self.lock.acquire()
                        potentialEvent = pygame.event.wait(1)
                        self.lock.release()
                        if potentialEvent.type != pygame.NOEVENT:
                            potentialEvent.time = pygame.time.get_ticks()
                            self.tempQueue.append(potentialEvent)
                else:
                    self.lock.acquire()
                    nextEvent = pygame.event.wait(10)
                    self.lock.release()
                    if nextEvent.type != pygame.NOEVENT:
                        nextEvent.time = pygame.time.get_ticks()
                        self.tempQueue.append(nextEvent)

                if self.recaptionNeeded:
                    with self.captionLock:
                        pygame.display.set_caption(self.caption)
                        self.recaptionNeeded = False
        except BaseException as e:
            print(e.__traceback__)
            raise(e)

    def getEvents(self) -> list:
        response = []
        if self.lock.acquire():
            for e in self.eventQueue:
                response.append(e)
            self.eventQueue.clear()
            self.lock.release()
        return response

    def stop(self):
        self.continuing = False
        

    def recaption(self, newName : str):
        with self.captionLock:
            self.recaptionNeeded = True
            self.caption = newName
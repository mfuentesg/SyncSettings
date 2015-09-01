# -*- coding: utf-8 -*-

def getDifference (setA, setB):
  return filter(lambda el: el not in setB, setA)


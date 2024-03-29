#!/usr/bin/env python3
# 
# Interview Scheduler
# Ford-Fulkerson algorithm to solve maximum flow
# 
# Acknowledgements:
# - Implementation of Ford-Fulkerson algorithm adapted from Wikipedia
# - Calendar from FullCalendar (http://fullcalendar.io/)
# 
# Vivek Sant
# 2014-09-23
# 

import sys
import time, datetime
from dateutil.parser import parse

FILE = sys.argv[1]

def txt_to_dt(x):
  return parse(x, fuzzy=True)

def dt_to_txt(x):
  return x.strftime('%a %m/%d/%y')

class Edge(object):
  def __init__(self, u, v, w):
    self.source = u
    self.sink = v
    self.capacity = w
  def __repr__(self):
    return "%s -> %s" % (self.source, self.sink)

class FlowNetwork(object):
  def __init__(self):
    self.adj = {}
    self.flow = {}

  def add_vertex(self, vertex):
    if vertex not in list(self.adj.keys()):
      self.adj[vertex] = []

  def get_edges(self, v):
    return self.adj[v]

  def add_edge(self, u, v, w=0):
    if u == v:
      raise ValueError("u == v")
    edge = Edge(u,v,w)
    redge = Edge(v,u,0)
    edge.redge = redge
    redge.redge = edge
    edgematches = [x for x in self.adj[u] if (x.source == u and x.sink == v and x.capacity == w)]
    if len(edgematches) == 0:
      self.adj[u].append(edge)
      self.adj[v].append(redge)
      self.flow[edge] = 0
      self.flow[redge] = 0

  def find_path(self, source, sink, path):
    if source == sink:
      return path
    for edge in self.get_edges(source):
      residual = edge.capacity - self.flow[edge]
      if residual > 0 and edge not in path:
        result = self.find_path( edge.sink, sink, path + [edge]) 
        if result != None:
          return result

  def max_flow(self, source, sink):
    path = self.find_path(source, sink, [])
    while path != None:
      residuals = [edge.capacity - self.flow[edge] for edge in path]
      flow = min(residuals)
      for edge in path:
        self.flow[edge] += flow
        self.flow[edge.redge] -= flow
      path = self.find_path(source, sink, [])

    output = ""
    alldates = []
    for edge in self.get_edges('s'):
      for i in reversed(sorted(self.get_edges(edge.sink), key=lambda r: self.flow[r])):
        if self.flow[i] == 1:
          if edge.sink[-1] == '*':
            color = 'green'
          else:
            color = 'red'
          output += "{ title: '%s', start: '%s', color:'%s' }," % (edge.sink, txt_to_dt(i.sink).strftime('%Y-%m-%d'), color)
          alldates.append(txt_to_dt(i.sink))
        if self.flow[i] == 0 and i.sink != 's':
          output += "{ title: '%s (alt)', start: '%s', color:'blue' }," % (edge.sink, txt_to_dt(i.sink).strftime('%Y-%m-%d'))
          alldates.append(txt_to_dt(i.sink))
    print("[" + output + "]|", end=' ')
    # Print mindate (default date to start calendar on)
    print(max(min(alldates), datetime.datetime.now()).strftime('%Y-%m-%d') + "|")
    # Print programs without matches
    for edge in self.get_edges('s'):
      if len([x for x in self.get_edges(edge.sink) if self.flow[x]==1]) == 0:
        print(edge.sink + "|")
g = FlowNetwork()
g.add_vertex('s')
g.add_vertex('t')

# Read in the data file of programs and possible dates
data = open(FILE).read().strip().split('\n')
for row in data:
  try:
    if row[:2] == '//':
      continue
    prog, datearr = [x.strip() for x in row.split('-')]
    g.add_vertex(prog)
    g.add_edge('s', prog, 1)
    for i in [x.strip() for x in datearr.strip().strip(',').strip().split(',')]:
      cleaned_date = dt_to_txt(txt_to_dt(i))
      g.add_vertex(cleaned_date)
      g.add_edge(prog, cleaned_date, 1)
      g.add_edge(cleaned_date, 't', 1)
  except:
    pass
g.max_flow('s','t')

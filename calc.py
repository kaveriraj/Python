#!/usr/bin/python
#INFIX to POSTFIX conversion in Python which reads from the input from a file
#Author - Kaveri Krishnaraj
import sys,os
stack = []
infix = []
postfix = []
temp = []

def main() :
   if len( sys.argv ) < 2 :  # read stdin
      f = sys.stdin.readline()
   else :
      f = open(sys.argv[1], 'r')

   infix2postfix( f )
   evalPostfix()
def infix2postfix( fin ) :

   for t in fin :
      infix = t.strip()
      #print t
      infix = t.split()
      infix.append(")")
      stack.append("(")
      for i in infix :
         if i == "(" :
               stack.append("(")
         elif i == ")" :
            temp = stack.pop()
            while temp is not '(' :
               postfix.append(temp)
               temp = stack.pop()
         elif i == '+' or i == '-' or i == '*' or i == '/' or i == '%' :
            p = precedence(i)
            while len(stack) is not 0 and p <= precedence(stack[-1]) :
               postfix.append(stack.pop())
            stack.append(i)
         else:
            postfix.append(i)
   while len(stack) > 0:
      postfix.append(stack.pop())
   #print ''.join(postfix)

def evalPostfix() :
   for i in postfix :
         if i == '+' or i == '-' or i == '*' or i == '/' or i == '%' :
            y = stack.pop()
	    x = stack.pop()

            stack.append( calc(i,x,y))

         else :

            stack.append(i)



   print ''.join(postfix) + "=" +str(stack)



def calc(op,x,y) :

   x = float(x)

   y = float(y)

   ret = 0.0

   if(op == "+") :

      ret = x + y

   elif(op == "-") :

      ret = x - y

   elif(op == "*") :

      ret = x * y

   elif(op == "/") :

      ret = x / y

   else :

      ret = x % y

   return ret

def precedence(k) :

   if k is '(':

      k = 0

   elif k is '+' or k is '-':

      k = 1

   elif k is '*' or k is '/' or k is '%':

      k = 2

   else:

      k = 99

   return k



                       

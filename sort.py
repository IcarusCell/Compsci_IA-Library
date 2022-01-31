
#--The partition and quicksort functions work together
#to perform a quicksort algorithm. The partition function
#checks to see if the first letter of the element j is
#after or before the first letter of the pivot. If it comes
#after, then it is moved to the back of the list. If it comes
#before it is moved towards the front. This is then recursively
#called through the quickSort function calling itself.--
def partition(initialArray,low,high):
   i = ( low-1 )
   pivot = initialArray[high]
   for j in range(low , high):
      if ord(initialArray[j][0]) <= ord(pivot[0]):
         i = i+1
         initialArray[i],initialArray[j] = initialArray[j],initialArray[i]
   initialArray[i+1],initialArray[high] = initialArray[high],initialArray[i+1]
   return ( i+1 )


def quickSort(initialArray,low,high):
   if low < high:
      split = partition(initialArray,low,high)
      quickSort(initialArray, low, split-1)
      quickSort(initialArray, split+1, high)

#--This function is used to call the quicksort, taking in
#an array of strings and sorting them alphabetically.--
def sort (initialArray):
   low = 0
   high = len(initialArray)-1
   quickSort(initialArray, low, high)
   return initialArray
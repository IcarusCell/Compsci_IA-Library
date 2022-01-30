# divide function
def partition(arr,low,high):
   i = ( low-1 )
   pivot = arr[high] # pivot element
   for j in range(low , high):
      # If current element is smaller
      if ord(arr[j][0]) <= ord(pivot[0]):
         # increment
         i = i+1
         arr[i],arr[j] = arr[j],arr[i]
   arr[i+1],arr[high] = arr[high],arr[i+1]
   return ( i+1 )
# sort
def quickSort(arr,low,high):
   if low < high:
      # index
      pi = partition(arr,low,high)
      # sort the partitions
      quickSort(arr, low, pi-1)
      quickSort(arr, pi+1, high)


def sort (arr):
   low = 0
   high = len(arr)-1
   quickSort(arr, low, high)
   return arr
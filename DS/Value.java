
class Value{
    public static void main(String[] args)
    {
        int arr[] = {15,2,2,4,7};
        boolean found = false;
        for(int i=0;i<arr.length;i++)
        {
            if(arr[i]==i)
            {
                System.out.println(i);
                found = true;
            }
        }
         if (!found) {
            System.out.println("No fixed point found");
        }
    }
}
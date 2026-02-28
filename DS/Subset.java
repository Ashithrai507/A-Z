class Subset{
    public static void main(String[] args)
    {
        int arr[] = {11,7,1,13,21,3,7,3};
        int sub[] = {11,3,7,1,7};
        int count = 0;
        int newarr = sub.length;

        for (int i = 0; i < sub.length; i++) {
            boolean found = false;
            for (int j = 0; j < arr.length; j++) {
                if (sub[i] == arr[j]) {
                    found = true;
                    break;
                }
            }
            if (found) {
                count++;
            } else {
                break;
            }
        }

        if (newarr == count)
        {
            System.out.println("true");
        }
        else{
            System.out.println("false");
        }
    }
}
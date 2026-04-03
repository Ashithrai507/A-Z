public class Perm {
    public static void main(String[] ashith)
    {
        String s1 = "abc";
        String s2 = "lecabee";
        int left = 0, right = s1.length(), count = 0;
        int windowsize = s2.length();
        while(right<s2.length())
        {
            for(int i=0;i<s1.length();i++)
            {
                if(s1.charAt(i)==s2.charAt(left))
                {
                    count++;
                    left++;
                }
                
            }
        }
         System.out.println("Not Found");
    }
}

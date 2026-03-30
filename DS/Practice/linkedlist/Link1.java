import java.util.LinkedList;

public class Link1 {
    public static void main(String[] args)
    {
        LinkedList<String> list = new LinkedList<>();
        int n=5;
        for (int i = 0; i < n; i++)
        {
            System.out.println("Enter a string: ");
            String str = System.console().readLine();
            list.add(str);
        }
        for (int i = 0; i < list.size(); i++)
        {
            System.out.println(list.get(i));
        }
    }
}

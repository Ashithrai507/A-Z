import java.util.LinkedList;

class Listmiddle {
    public static void main(String[] args) {
        
        LinkedList<String> list = new LinkedList<>();
        list.add("ashith");
        list.add("hello");
        list.add("hello1");
        list.add("hello2");
        list.add("hello1");
        int left = 0;
        int right = 0;
        while(right<=list.size()-1)
        {
            left += 1;
            right += 2;
        }
        System.out.println(list.get(left));

    }
}
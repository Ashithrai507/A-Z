public class Length {
    public static void main(String[] args)
    {
        Node head = new Node(10);
        Node second = new Node(20);
        Node third = new Node(30);

        head.next = second;
        second.next = third;  
        
        int length = 0;
        Node current = head;
        while(current != null)
        {            length++;
            current = current.next;
        }
        System.out.println("Length of the linked list: " + length);
    }
    
}

class Node{
    int data;
    Node next;

    Node(int d)
    {
        data = d;
        next = null;
    }
}

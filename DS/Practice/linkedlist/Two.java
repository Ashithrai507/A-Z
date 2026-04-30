import org.w3c.dom.Node;

public class Two {
    Node head1 = new Node(10);
    head1.next = new Node(20);

    Node head2 = new Node(30);
    head2.next = new Node(40);

     System.out.println("Length of List 1: " + getCount(head1));
    System.out.println("Length of List 2: " + getCount(head2));
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

class End {
    public static void main(String[] args) {
    Node head = new Node(10);
    head.next = new Node(20);
    head.next.next = new Node(30);
    head.next.next.next = new Node(40);
    int k = 2;
    
    int length = 0; 
    Node current = head;
    while(current != null)
    {
        length ++;
        current = current.next;
    }
    
    int targetIndex = length - k; 
    current = head;
    
    for(int i = 0; i < targetIndex; i++) {
        current = current.next;
    }
    System.out.println(current.data);
    }
}
class Node{
    int data;
    Node next;
    
    Node(int d){
        data = d;
        next = null;
    }
}
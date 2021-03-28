package com.guanguan;

public class Test {
    public static void main(String[] args) {
        String[][] strings = {{"O1-7", "2017110101", "否", "2019-06-12", "2019-07-12"},
                {"O1-7", "2017110101", "否", "2019-06-12", "2019-07-12"},
                {"O1-7", "2017110101", "否", "2019-06-12", "2019-07-12"}};
        String[] head = {"bookid", "Rno","isback", "borrowDate", "backDate"};

        TableVis tableVis = new TableVis(strings);
        tableVis.setHead(head);
        System.out.println(tableVis);
    }
}

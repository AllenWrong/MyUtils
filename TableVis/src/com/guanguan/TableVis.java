package com.guanguan;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * @author Andrew guan
 * @version 1.0
 */
public class TableVis {
    private Object[][] objects;
    private Object[] head;
    private HashMap<Integer, Integer> colSizeMap;
    private String visualTable;
    private String firstLine;


    /**
     * Object can be String or Integer.
     * @param objects
     */
    public TableVis(Object[][] objects) {
        if (objects instanceof String[][] || objects instanceof Integer[][]) {
            this.objects = objects;
            this.colSizeMap = new HashMap<>();
            this.head = null;
            this.visualTable = "";
        } else {
            throw new RuntimeException("Unsupport data type. Only String[][] and Integer[][] is supported.");
        }
    }

    /**
     * Set the data of table head if any.
     * @param head data.
     */
    public void setHead(Object[] head) {
        if (head.length != this.objects[0].length) {
            throw new RuntimeException("The field's number of the head is not equal the column's number of the 2d-array.");
        } else {
            this.head = head;
        }
    }

    /** Get the max width of every column. */
    private void getMaxWidthOfCol() {
        for (int i = 0; i < this.objects[0].length; i++) {
            int max = 0;
            for (int j = 0; j < this.objects.length; j++) {
                String str = this.objects[j][i].toString();

                int length = getLen(str);
                if (length > max) {
                    max = length;
                }

                String headStr = this.head[i].toString();

                length = getLen(headStr);
                if (length > max) {
                    max = length;
                }
            }
            this.colSizeMap.put(i, max + 2);
        }
    }

    /**
     * Get the length of string. There maybe exists chinese character.
     * @param str
     * @return
     */
    private int getLen(String str) {
        // Count the length of character.
        int length = 0;
        char[] chars = str.toCharArray();
        for (int k = 0; k < chars.length; k++) {
            String len = Integer.toBinaryString(chars[k]);
            if (len.length() > 8) {
                length += 2;
            } else {
                length += 1;
            }
        }
        return length;
    }

    /**
     * Build the first line. ('+---+---+---+')
     */
    private void buildFirstLine() {
        String line = "+";
        Set<Map.Entry<Integer, Integer>> entrySet = this.colSizeMap.entrySet();
        for (Map.Entry<Integer, Integer> entry : entrySet) {
            for(int i = 0; i < entry.getValue(); i++) {
                line += "-";
            }
            line += "+";
        }
        this.firstLine = line;
    }

    /**
     * Build the head part if any.
     */
    private void buildHead() {
        if (null != this.head) {
            this.visualTable += this.firstLine + "\n";
            this.visualTable += buildARow(this.head) + "\n";
        }
    }

    /**
     * Convert a row in the 2d-array to one line String.
     * @param row
     * @return
     */
    private String buildARow(Object[] row) {
        String string = "|";
        for (int i = 0; i < row.length; i++) {
            int width = this.colSizeMap.get(i);
            String subStr = " " + row[i];
            while (getLen(subStr) < width) {
                subStr += " ";
            }
            string += subStr + "|";
        }
        return string += " ";
    }

    /**
     * Main build method.
     */
    private void build() {
        getMaxWidthOfCol();
        buildFirstLine();
        buildHead();

        this.visualTable += firstLine + "\n";
        for (int i = 0; i < this.objects.length; i++) {
            String row = buildARow(this.objects[i]);
            this.visualTable += row + "\n";
        }
        this.visualTable += firstLine += "\n";
    }

    @Override
    public String toString() {
        build();
        return this.visualTable;
    }
}

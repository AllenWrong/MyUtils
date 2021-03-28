package andrewguan;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Set;

/**
 * The main class of the module. To validate if a plan of schema decomposition
 * is loss less, you can do the following operation:<br/>
 *  1. use input function to input the data. You can reference the test.txt when
 *     you write your input file. The specific description of the file is in the
 *     test.txt.<br/>
 *  2. use the validate function to validate.
 * @author Thingcor
 * @version 1.0
 *
 */
public class LossLessValidation {
	private R r;
	private F f;
	private Rho rho;
	private String[][] table;
	
	public LossLessValidation() {
		this.r = new R();
		this.f = new F();
		this.rho = new Rho();
	}
	
	public void input(File file) {
		try {
			FileInputStream inputStream = new FileInputStream(file);
			BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
			String line = reader.readLine();
			r.input(line);
			
			int n = Integer.parseInt(reader.readLine());
			String[] fstr = new String[n];
			for (int i = 0; i < n; i++) {
				fstr[i] = reader.readLine();
			}
			f.input(fstr);
			n = Integer.parseInt(reader.readLine());
			String[] rhostr = new String[n];
			for (int i = 0; i < n; i++) {
				rhostr[i] = reader.readLine();
			}
			rho.input(rhostr);
			reader.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		constructTable();
	}
	
	public void printR() {
		System.out.println(r);
	}
	
	public void printF() {
		System.out.println(f);
	}
	
	public void printRho() {
		System.out.println(rho);
	}
	
	public void print() {
		System.out.println(r);
		System.out.println(f);
		System.out.println(rho);
	}
	
	public void validate() {
		if (update()) {
			System.out.println("This is a loss less.");
		} else {
			System.out.println("This is not loss less.");
		}
	}
	
	private void constructTable() {
		table = new String[rho.getLength()][rho.getLength()];
		for (int i = 0; i < table.length; i++) {
			String key = rho.getKey(i);
			for (int j = 0; j < table[i].length; j++) {
				if (rho.containValue(key, r.getList().get(j))) {
					table[i][j] = "a" + (j+1);
				} else {
					table[i][j] = "b" + (i+1) + (j+1);
				}
			}
		}
	}
	
	/**
	 * Get the specific column of every row in the table.
	 * @param leftPart A string containing all the column name that needed
	 *                 to get.
	 * @return A linked hash map. 
	 *            key : index of the row. 
	 *            value : a string containing the column value that we needed.
	 */
	private LinkedHashMap<Integer, String> getSubTuple(String leftPart){
		ArrayList<Integer> indexList = new ArrayList<>();
		/*
		 * Get the column names from the string. And convert it into
		 * index.
		 */
		for (int i = 0; i < leftPart.length(); i++) {
			String ch = leftPart.charAt(i) + "";
			indexList.add(r.getIndex(ch));
		}
		
		LinkedHashMap<Integer, String> map = new LinkedHashMap<>();
		/*
		 * Get the specific column value of every line. One string
		 * contains all the column value of one line.
		 */
		for (int i = 0; i < table.length; i++) {
			String line = "";
			for (Integer index : indexList) {
				line += table[i][index];
			}
			map.put(i, line);
		}
		
		return map;
	}
	
	private void changeRightPart(LinkedHashMap<Integer, String> subTuple, String rightPart) {
		Sort sort = new Sort(subTuple.entrySet());
		ArrayList<ArrayList<Integer>> rowIndexList =  sort.getEqIndexList();
		
		/*
		 * Get the column names from the string. And convert it into
		 * index.
		 */
		ArrayList<Integer> indexList = new ArrayList<>();
		for (int i = 0; i < rightPart.length(); i++) {
			String ch = rightPart.charAt(i) + "";
			indexList.add(r.getIndex(ch));
		}
		
		// Iterate the column index contained in the index list.
		for (int col = 0; col < indexList.size(); col++) {
			// Iterate the inner list which contains the row index.
			for (int i = 0; i < rowIndexList.size(); i++) {
				ArrayList<String> rightPartValue = new ArrayList<>();
				ArrayList<Integer> innerList = rowIndexList.get(i);
				// Iterate the row index.
				for(int j = 0; j < innerList.size(); j++) {
					// Add the right part value to the list. One column per time.
					String value = table[innerList.get(j)][indexList.get(col)];
					rightPartValue.add(value);
				}
				
				// Judge if the right part exist "a..".
				boolean exist = false;
				String newRightValue = "";
				for (int j = 0; j < rightPartValue.size(); j++) {
					if (rightPartValue.get(j).indexOf("a") != -1) {
						newRightValue = rightPartValue.get(j);
						exist = true;
						break;
					}
				}
				
				// If there does not exist "a..", use the first value.
				if (exist) {
					for (int j = 0;j < innerList.size(); j++) {
						table[innerList.get(j)][indexList.get(col)] = newRightValue;
					}
				} else {
					newRightValue = rightPartValue.get(0);
					for (int j = 0;j < innerList.size(); j++) {
						table[innerList.get(j)][indexList.get(col)] = newRightValue;
					}
				}
			}
		}
	}
	
	private boolean update() {
		Set<String> keys = f.getKeys();
		for (String key : keys) {
			String leftPart = key;
			String rightPart = f.get(key);
			changeRightPart(getSubTuple(leftPart), rightPart);
			if (checkA()) {
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Check if there exists an row that all element of it is "a..".
	 * @return true if exists else false.
	 */
	private boolean checkA() {
		boolean flag = true;
		for (int i = 0; i < rho.getLength(); i++) {
			for (int j = 0; j < r.getLength(); j++) {
				if (!table[i][j].equals("a" + (j+1))) {
					flag = false;
				}
			}
			if (flag) {
				return flag;
			} else if (i != rho.getLength() - 1) {
				flag = true;
			}
		}
		return flag;
	}
}

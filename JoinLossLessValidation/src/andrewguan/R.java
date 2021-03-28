package andrewguan;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class R {
	/**
	 * Core data structure of this class. It contains all the element
	 * that the 'r' has.
	 */
	private ArrayList<String> list;
	
	public R() {
		this.list = new ArrayList<>();
	}
	
	/**
	 * User can use this function to get the input from console.
	 */
	public void input() {
		BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
		try {
			System.out.println("Please input all the properties: (like A B C)");
			String[] strings = reader.readLine().split(" ");
			for(String string : strings) {
				this.list.add(string);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * This function is called by LossLessValidation.java.
	 * @param line all the element of the 'R'. Split with " ".
	 */
	public void input(String line) {
		String[] strings = line.split(" ");
		for(String string : strings) {
			this.list.add(string);
		}
	}
	
	/**
	 * Get element by index.
	 * @param index
	 * @return
	 */
	public String get(int index) {
		return this.list.get(index);
	}
	
	/**
	 * Get the index of specific element.
	 * @param string the element that you need to get index.
	 * @return
	 */
	public int getIndex(String string) {
		for (int i = 0; i < this.list.size(); i++) {
			if (this.list.get(i).equals(string)) {
				return i;
			}
		}
		return -1;
	}
	
	/**
	 * Get the length of the inner list.
	 * @return
	 */
	public int getLength() {
		return this.list.size();
	}
	
	public ArrayList<String> getList() {
		return this.list;
	}

	@Override
	public String toString() {
		String result = "R={";
		int i = 0;
		for(String string : list) {
			i++;
			result += string;
			if (i != list.size()) {
				result += " ";
			}
		}
		return result + "}";
	}
}

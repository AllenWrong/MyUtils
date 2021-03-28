package andrewguan;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedHashMap;
import java.util.Map.Entry;
import java.util.Set;

public class F {
	/**
	 * Key: the left part of the formula.
	 * Value: the right part of the formula. <br/>
	 */
	private LinkedHashMap<String, String> map;
	
	public F() {
		this.map = new LinkedHashMap<>();
	}
	
	/**
	 * User can input from console use this function. But I do not recommend
	 * you to use this function.
	 */
	public void input() {
		BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
		try {
			System.out.println("Please input the number of the function dependences:");
			int num = Integer.parseInt(reader.readLine());
			for (int i = 0; i < num; i++) {
				System.out.println("Please input the " + (i+1) + "-th function dependeces: (like A→C)");
				String line = reader.readLine();
				String[] strings = line.split("→");
				this.map.put(strings[0], strings[1]);
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * This function is called by the input function of LossLessValidation.java
	 * @param lines An array contains all the lines that needed to input.
	 */
	public void input(String[] lines) {
		for (int i = 0; i < lines.length; i++) {
			String[] strings = lines[i].split("→");
			this.map.put(strings[0], strings[1]);
		}
	}
	
	/**
	 * @return the length of the inner map.
	 */
	public int getLength() {
		return this.map.size();
	}
	
	public Set<String> getKeys() {
		return this.map.keySet();
	}
	
	/**
	 * Get key by index.
	 * @param index the index of key that you needed.
	 * @return key.
	 */
	public String getKey(int index) {
		Set<String> ketSet = this.map.keySet();
		int i = 0;
		String result = "";
		for (String string : ketSet) {
			if (i == index) {
				result += string;
				break;
			}
			i++;
		}
		return result;
	}
	
	/**
	 * Get value of map by key.
	 * @param key
	 * @return
	 */
	public String get(String key) {
		return this.map.get(key);
	}
	
	/**
	 * Get the index of a key.
	 * @param key
	 * @return index. If this map does not contain the key
	 *          it will return -1.
	 */
	public int getKeyIndex(String key) {
		Set<String> ketSet = this.map.keySet();
		int i = 0;
		for (String string : ketSet) {
			if (string.equals(key)) {
				return i;
			} else {
				i++;
			}
		}
		return -1;
	}
	
	/**
	 * Get the index of value.
	 * @param value
	 * @return index. If this map does not contain the key
	 *          it will return -1.
	 */
	public int getValueIndex(String value) {
		Set<String> ketSet = this.map.keySet();
		int i = 0;
		for (String string : ketSet) {
			if (this.map.get(string).equals(value)) {
				return i;
			} else {
				i++;
			}
		}
		return -1;
	}

	@Override
	public String toString() {
		String label = "→";
		String result = "F={";
		Set<Entry<String, String>> set = map.entrySet();
		int i = 0;
		for(Entry<String, String> entry : set) {
			i++;
			result += entry.getKey() + label + entry.getValue() ;
			if (i != set.size()) {
				result += " ";
			}
		}
		return result + "}";
	}
}

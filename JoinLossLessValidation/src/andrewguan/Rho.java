package andrewguan;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.LinkedHashMap;
import java.util.Map.Entry;
import java.util.Set;

/**
 * It represents a plan of mode decomposition.
 * @author Thingcor
 *
 */
public class Rho {
	/**
	 * Key: sub-schema name.
	 * Value: properties name.
	 */
	private LinkedHashMap<String, String> map;
	
	public Rho() {
		this.map = new LinkedHashMap<>();
	}
	
	/**
	 * User can use this function to get the input from console.
	 */
	public void input() {
		BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
		try {
			System.out.println("Please input the number of the sub-schema:");
			int num = Integer.parseInt(reader.readLine());
			for (int i = 0; i < num; i++) {
				System.out.println("Please input the " + (i+1) + "-th sub-schema: (like R1(A,B))");
				String line = reader.readLine();
				// Get the name of the sub-schema, use the name as the key of map.
				String key = line.substring(0, line.indexOf("("));
				
				// Get the sub-string "A,B" and throw the ",", then use the "AB" as the value of map. 
				String[] values = line.substring(line.indexOf("(") + 1, line.indexOf(")")).split(",");
				String value = "";
				for(String string : values) {
					value += string;
				}
				this.map.put(key, value);
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * This function is called by LossLessValidation.java.
	 * @param lines
	 */
	public void input(String[] lines) {
		for (int i = 0; i < lines.length; i++) {
			// Get the name of the sub-schema, use the name as the key of map.
			String key = lines[i].substring(0, lines[i].indexOf("("));
			
			// Get the sub-string "A,B" and throw the ",", then use the "AB" as the value of map. 
			String[] values = lines[i].substring(lines[i].indexOf("(") + 1, lines[i].indexOf(")")).split(",");
			String value = "";
			for(String string : values) {
				value += string;
			}
			this.map.put(key, value);
		}
	}
	
	/**
	 * Get the length of the inner map.
	 * @return
	 */
	public int getLength() {
		return this.map.size();
	}
	
	/**
	 * Judge if the inner map contains a substring.
	 * @param key
	 * @param str
	 * @return
	 */
	public boolean containValue(String key, String str) {
		return this.map.get(key).indexOf(str) != -1;
	}
	
	/**
	 * Get key set.
	 * @return
	 */
	public Set<String> getKeys() {
		return this.map.keySet();
	}
	
	/**
	 * Get key by the index.
	 * @param index index of key.
	 * @return
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
	 * Get the index of the specific key.
	 * @param key
	 * @return
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
	
	@Override
	public String toString() {
		String result = "Rho={";
		String line = "";
		Set<Entry<String, String>> set = this.map.entrySet();
		int k = 0;
		for(Entry<String, String> entry : set) {
			k++;
			String value = "";
			for(int i = 0; i < entry.getValue().length(); i++) {
				value += entry.getValue().charAt(i);
				if (i != entry.getValue().length()-1) {
					value += ",";
				}
			}
			line += entry.getKey() + "(" + value + ")";
			if (k != set.size()) {
				line += " ";
			}
		}
		
		return result + line +"}";
	}
}

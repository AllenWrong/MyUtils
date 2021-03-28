package andrewguan;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Map.Entry;

import java.util.Set;

public class Sort {
	/**
	 * By using the list of entry, we can do sort operation conveniently.
	 * key of entry : 
	 * value of entry : 
	 */
	private ArrayList<Entry<Integer, String>> list;
	
	public Sort(Set<Entry<Integer, String>> set) {
		this.list = new ArrayList<>();
		for(Entry<Integer, String> entry : set) {
			list.add(entry);
		}
		sort();
	}
	
	/**
	 * Helper function. Do sort operation.
	 */
	private void sort() {
		Collections.sort(list, new Comparator<Entry<Integer, String>>() {
			@Override
			public int compare(Entry<Integer, String> o1, Entry<Integer, String> o2) {
				return o1.getValue().compareTo(o2.getValue());
			}
		});
	}
	
	/**
	 * This is a helper function but I set it with "public" for test reason.<br/>
	 * Get a index list. This list contains some array. An array in this
	 * list represents an segment whose line is all equal.
	 * Such as some column of a table:
	 * <table>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>a1</td><td>b22</td></tr>
	 * <tr><td>b13</td><td>a2</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>b13</td><td>b23</td></tr>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>b13</td><td>a2</td></tr>
	 * </table>
	 * 
	 * It will become the following form after it is sorted.
	 * <table>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>a1</td><td>a2</td></tr>
	 * <tr><td>a1</td><td>b22</td></tr>
	 * <tr><td>b13</td><td>a2</td></tr>
	 * <tr><td>b12</td><td>a2</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * </table>
	 * 
	 * The following segment will be use an array[7,3, str] to represent.
	 * The first element is base index 7.
	 * The second element is offset 3.
	 * The last element will be add later.
	 * <table>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * <tr><td>b14</td><td>b24</td></tr>
	 * </table>
	 * 
	 * @return list of array.
	 */
	public ArrayList<Object[]> getEqSegmentDescripList() {
		int offset = 1;
		int base = 0;
		
		ArrayList<Object[]> result = new ArrayList<>();
		for (int i = 0; i < list.size() - 1; i++) {
			int j = i;
			while (j < list.size() - 1 && list.get(j).getValue().equals(list.get(++j).getValue())) {
				offset++;
			}
			
			if (offset > 1) {
				Object[] objects = new Object[3];
				objects[Index.INDEX_BASE] = base;
				objects[Index.INDEX_NUM] = offset;
				result.add(objects);
				i = (base + offset - 1);
				base = i + 1;
				offset = 1;
			} else {
				base++;
			}
		}
		
		return result;
	}
	
	/**
	 * Get the key of every equal segment.
	 * @return An list of list. The inner list contains all the index in a equal segment.
	 */
	public ArrayList<ArrayList<Integer>> getEqIndexList() {
		ArrayList<ArrayList<Integer>> result = new ArrayList<>();
		
		ArrayList<Object[]> objList = getEqSegmentDescripList();
		for (int i = 0; i < objList.size(); i++) {
			// Get the base index and the offset.
			Object[] objects = objList.get(i);
			int base = (int) objects[Index.INDEX_BASE];
			int offset = (int) objects[Index.INDEX_NUM];
			
			// Put the key(index of row) into the inner list.
			ArrayList<Integer> innerList = new ArrayList<>();
			for (int j = base; j < (base + offset); j++) {
				innerList.add(list.get(j).getKey());
			}
			// put the inner list into the result list.
			result.add(innerList);
		}
		
		return result;
	}
	
	public static interface Index {
		public static final int INDEX_BASE = 0;
		public static final int INDEX_NUM = 1;
		public static final int INDEX_STRING = 2;
	}
}
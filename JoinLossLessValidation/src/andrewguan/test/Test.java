package andrewguan.test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map.Entry;

import andrewguan.LossLessValidation;
import andrewguan.Sort;

public class Test {
	
//	public static void testLossLessValidation() {
//		LossLessValidation lessValidation = new LossLessValidation();
//		File file = new File("./src/test.txt");
//		lessValidation.input(file);
//		lessValidation.validate();
//	}
//	
//	public static void testGetSubTuple() {
//		LossLessValidation lessValidation = new LossLessValidation();
//		lessValidation.input(new File("./src/test.txt"));
//		
//		LinkedHashMap<Integer, String> map1 = lessValidation.getSubTuple("A");
//		LinkedHashMap<Integer, String> map1Test = new LinkedHashMap<>();
//		map1Test.put(0, "a1");
//		map1Test.put(1, "a1");
//		map1Test.put(2, "b31");
//		map1Test.put(3, "b41");
//		map1Test.put(4, "a1");
//		System.out.println("Test map1 :" + mapEqual(map1, map1Test));
//		
//		LinkedHashMap<Integer, String> map2 = lessValidation.getSubTuple("AB");
//		LinkedHashMap<Integer, String> map2Test = new LinkedHashMap<>();
//		map2Test.put(0, "a1b12");
//		map2Test.put(1, "a1a2");
//		map2Test.put(2, "b31a2");
//		map2Test.put(3, "b41b42");
//		map2Test.put(4, "a1b52");
//		System.out.println("Test map2 :" + mapEqual(map2, map2Test));
//	
//	}
//	
//	private static boolean mapEqual(LinkedHashMap<Integer, String> map1, LinkedHashMap<Integer, String> map2) {
//		Iterator<Entry<Integer, String>> iterator1 = map1.entrySet().iterator();
//		Iterator<Entry<Integer, String>> iterator2 = map2.entrySet().iterator();
//		
//		if (map1.entrySet().size() != map2.entrySet().size()) {
//			return false;
//		}
//		
//		while(iterator1.hasNext()) {
//			Entry<Integer, String> entry1 = iterator1.next();
//			Entry<Integer, String> entry2 = iterator2.next();
//			boolean flag = entry1.getKey().equals(entry2.getKey()) && entry1.getValue().equals(entry2.getValue());
//			if (!flag) {
//				return false;
//			}
//		}
//		
//		return true;
//	}
//	
//	public static boolean testSort() throws IOException {
//		File file = new File("./src/testSort.txt");
//		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
//		String firstLine = reader.readLine();
//		int rowNum = Integer.parseInt(firstLine);
//		
//		LinkedHashMap<Integer, String> map = new LinkedHashMap<>();
//		for (int i = 0; i < rowNum; i++) {
//			map.put(i, reader.readLine());
//		}
//		reader.close();
//		
//		Sort sort = new Sort(map.entrySet());
//		ArrayList<Object[]> list = sort.getEqSegmentDescripList();
//		ArrayList<Object[]> listComp = new ArrayList<>();
//		listComp.add(new Object[] {0, 3, null});
//		listComp.add(new Object[] {4, 2, null});
//		listComp.add(new Object[] {7, 2, null});
//		
//		if (list.size() != listComp.size()) {
//			System.out.println("Test sort fail!");
//			return false;
//		} else {
//			for (int i = 0; i < list.size(); i++) {
//				Object[] objects = list.get(i);
//				Object[] objectsComp = listComp.get(i);
//				for (int j = 0; j < objects.length; j++) {
//					if (objects[j] != null && objectsComp[j] != null) {
//						if (!objects[j].equals(objectsComp[j])) {
//							System.out.println("Array is not equal.");
//							return false;
//						}
//					} else if (objects[j] == null && objectsComp[j] == null) {
//						
//					} else {
//						System.out.println("Array is not equal.");
//						return false;
//					}
//				}
//			}
//			
//			System.out.println("test sort pass.");
//			return true;
//		}
//	}
//	
//	public static void testGetEqIndexList() throws IOException {
//		File file = new File("./src/testSort.txt");
//		BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
//		String firstLine = reader.readLine();
//		int rowNum = Integer.parseInt(firstLine);
//		
//		LinkedHashMap<Integer, String> map = new LinkedHashMap<>();
//		for (int i = 0; i < rowNum; i++) {
//			map.put(i, reader.readLine());
//		}
//		reader.close();
//		
//		Sort sort = new Sort(map.entrySet());
//		ArrayList<ArrayList<Integer>> list = sort.getEqIndexList();
//		ArrayList<ArrayList<Integer>> listComp = new ArrayList<>();
//		Integer[] one = {0, 5, 7};
//		Integer[] two = {2, 8};
//		Integer[] three = {3, 4};
//		listComp.add(new ArrayList<>(Arrays.asList(one)));
//		listComp.add(new ArrayList<>(Arrays.asList(two)));
//		listComp.add(new ArrayList<>(Arrays.asList(three)));
//		
//		if (list.size() != listComp.size()) {
//			System.out.println("Length of Array is not equal. Test getEqIndexList fail.");
//			return;
//		} else {
//			for (int i = 0; i < list.size(); i++) {
//				ArrayList<Integer> tempList = list.get(i);
//				ArrayList<Integer> tempListComp = listComp.get(i);
//				if (tempList.size() != tempListComp.size()) {
//					System.out.println("Length of array " +  i + " is not equal. Test getEqIndexList fail.");
//					return;
//				} else {
//					for (int j = 0; j < tempList.size(); j++) {
//						if (!tempList.get(j).equals(tempListComp.get(j))) {
//							System.out.println("Element " + j + " of array " +
//						        i + " is not equal. Test getEqIndexList fail.");
//							return;
//						}
//					}
//				}
//			}
//		}
//		
//		System.out.println("Test getEqIndexList pass.");
//	}
	
	public static void main(String[] args) {
//		try {
//			Test.testGetSubTuple();
//			Test.testSort();
//			Test.testGetEqIndexList();
//			Test.testLossLessValidation();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
	}
}

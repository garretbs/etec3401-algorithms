/* File: EditDistanceExample.java
 * Date: 10/17/2016
 */

import java.io.*;
import java.util.ArrayList;
import java.awt.*;
import javax.swing.*;
import javax.swing.text.*;
import javax.swing.event.*;

public class EditDistanceExample
{
	// singleton pattern
	private static EditDistanceExample mInstance = null;
	
	private JFrame mFrame;
	private ArrayList<String> mWords; // array of English words
        private final int INF = (int) Double.POSITIVE_INFINITY;
	
	public synchronized static EditDistanceExample getInstance()
	{
		if (mInstance == null) mInstance = new EditDistanceExample();
		return mInstance;
	}
	
	private EditDistanceExample()
	{
		try
		{
			this.loadWords(); // load words from "wordsEn.txt"
		}
		catch (Exception e)
		{
			System.err.println("Error reading words: " + e);
			System.exit(1);
		}
				
		mFrame = new JFrame("Edit Distance Example");
		
		JTextArea textArea = new JTextArea();
		mFrame.add(textArea, BorderLayout.CENTER);
		
		textArea.getDocument().addDocumentListener(new DocumentListener()
			{
				Document document = textArea.getDocument();
				String currentWord = "";
				
				public void changedUpdate(DocumentEvent e)
				{
				}

				
				public void insertUpdate(DocumentEvent e)
				{
					try
					{
						// if spacebar was pressed, find closest word
						if (document.getText(e.getOffset(), 1).equals(" "))
						{
							EditDistanceExample editDist =
								EditDistanceExample.getInstance();
							System.out.println("Finding matches for " +
								currentWord);
							System.out.println("Found: " +
								editDist.getClosestWord(currentWord));
							currentWord = "";
						}
						else
						{
							currentWord += document.getText(e.getOffset(), 1);
						}
					}
					catch (BadLocationException ble)
					{
						System.err.println(ble);
						System.exit(1);
					}
				}
				
				public void removeUpdate(DocumentEvent e)
				{
				}
			});
		
		mFrame.setSize(400, 200);
		mFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		mFrame.setVisible(true);
	}
	
	// iterate through word list, returning the closest
	public String getClosestWord(String word)
	{
		int min = -1;
		String minWord = "";
		for (String dictWord : mWords)
		{
			if (min == -1)
			{
				min = this.wordDistance(dictWord, word,
					dictWord.length() - 1, word.length() - 1);
				minWord = dictWord;
			}
			else
			{
				int tmpDist = this.wordDistance(dictWord, word,
					dictWord.length() - 1, word.length() - 1);
				if (tmpDist < min)
				{
					min = tmpDist;
					minWord = dictWord;
				}
			}
		}
		
		return minWord;
	}
	
	// recursive implementation of edit distance algorithm
	/*private int wordDistance(String t, String p, int i, int j)
	{
		if (t == null || p == null) return -1;
		if (t.equals("")) return p.length();
		if (p.equals("")) return t.length();
		if (i == -1) return j + 1;
		if (j == -1) return i + 1;
		
		int mismatch = 1;
		if (t.charAt(i) == p.charAt(j)) mismatch = 0;
		
		int subOrMatch = wordDistance(t, p, i - 1, j - 1) + mismatch;
		int insert = wordDistance(t, p, i - 1, j) + 1;
		int delete = wordDistance(t, p, i, j - 1) + 1;
		
		return Math.min(subOrMatch, Math.min(insert, delete));
	}*/
        
    //dynamic programming implementation
	private int wordDistance(String t, String p, int i, int j)
	{
                if (t == null || p == null) return -1;
		if (t.equals("")) return p.length();
		if (p.equals("")) return t.length();
                
                //Calculate the values for the dynamic table
                int[][] dynamicTable = new int[i+1][j+1];
                int mismatch;
                int subOrMatch;
                int insert;
                int delete;
                for(int idx = 0; idx <= i; idx++){
                    for(int jdx = 0; jdx <= j; jdx++){
                        if(idx == 0 && jdx == 0){ //top left, no dependencies
                            dynamicTable[idx][jdx] = t.charAt(idx) == p.charAt(jdx) ? 0 : 1;
                        }else{
                            mismatch = t.charAt(idx) == p.charAt(jdx) ? 0 : 1;
                            subOrMatch = idx > 0 && jdx > 0 ? dynamicTable[idx-1][jdx-1] + mismatch : INF;
                            insert = idx > 0 ? dynamicTable[idx-1][jdx] + 1 : INF;
                            delete = jdx > 0 ? dynamicTable[idx][jdx-1] + 1 : INF;
                            dynamicTable[idx][jdx] = 1 + Math.min(subOrMatch, Math.min(insert, delete));  
                        }
                    }
                }
                return dynamicTable[i][j];
	}
        
	private void loadWords() throws FileNotFoundException, IOException
	{
		BufferedReader br = new BufferedReader(new FileReader("wordsEn.txt"));
		
		mWords = new ArrayList<String>();
		
		String inStr = br.readLine();
		while (inStr != null)
		{
			mWords.add(inStr);
			inStr = br.readLine();
		}
		
		br.close();
	}
	
	public static void main(String[] args)
	{
		EditDistanceExample.getInstance();
	}
}

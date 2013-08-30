package data;

import edu.mines.jtk.io.ArrayFile;
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteOrder;

/**
 * A class devoted to getting binary data from a specified file and possibly
 * shortening it if necessary. The files this class needs to have any headers
 * stripped from the data file and the data file should be in the Big Endian
 * format.
 * 
 * @author Chris Graziano
 */
public class SUDataGrabber {

	/**
	 * Gets 2D data from a file and puts it into a 2D array of floats.
   * works with su data only, not segy
	 * 
	 * @param fileLoc
	 *            ex) "C://Users/Chris/Documents/Data.dat" 
	 * @param n2
	 *            The number of samples in the slow dimension of the data.
	 * @param n1
	 *            The number of samples in the fast dimension of the data.
	 * @return The 2D data in a 2D array of floats.
	 */
	public static float[][] grab2DSuFile(String fileLoc, int n2, int n1) {
		float[][] data = new float[n2][n1];
    File file = new File("fileLoc");
    String fileName = file.getPath();

		try {
			ArrayFile af = new ArrayFile(fileName, "r", ByteOrder.BIG_ENDIAN,
					ByteOrder.LITTLE_ENDIAN);
			af.readFloats(data);

			System.out.println("Data extracted from " + fileName);

			af.close();

		} catch (IOException e) {
			System.out.println("File Cannot be found!");
			throw new RuntimeException(e);
		}

		return data;
	}

	

}

import java.util.ArrayList;

public class DTWDistance {
	public static double getDTWDistance(double[] s1, double[] s2, int w) {
		double[][] DTW = new double[s1.length][s2.length];
	    w = Math.max(w, Math.abs(s1.length- s2.length));
//	    prepare array
	    for (int i = 0; i < s1.length; i++) {
	        for (int j = 0; j < s2.length; j++) {
	            DTW[i][j] = Double.POSITIVE_INFINITY;
	        }
	    }
	    DTW[0][0] = 0;
//	    fill array with corresponding DTW values
	    for (int i = 1; i < s1.length; i++) {
	        for (int j = 1; j < s2.length; j++) {
	            double dist = Math.pow((s1[i]-s2[j]), 2);
	            DTW[i][j] = dist + Math.min(Math.min(DTW[i-1][j],DTW[i][j-1]), DTW[i-1][j-1]);
	        }
	    }
//	    return distance
	    return Math.sqrt(DTW[s1.length-1][s2.length-1]);
	}
}

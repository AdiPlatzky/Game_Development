using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.Collections;
using System.ComponentModel;
using System.Diagnostics.CodeAnalysis;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Serialization;
using System.Text.RegularExpressions;
using System.Text;
using System;

class Result
{

    /*
     * Complete the 'surfaceArea' function below.
     *
     * The function is expected to return an INTEGER.
     * The function accepts 2D_INTEGER_ARRAY A as parameter.
     */

    public static int surfaceArea(List<List<int>> A)
    {
        int H = A.Count, W = A[0].Count;
        int[] dr = { 1, -1, 0, 0 };
        int[] dc = { 0, 0, 1, -1 };
        int area = 0;

        for (int i = 0; i < H; i++)
        {
            for (int j = 0; j < W; j++)
            {
                int h = A[i][j];
                if (h > 0) area += 2;

                for (int d = 0; d < 4; d++)
                {
                    int ni = i + dr[d], nj = j + dc[d];
                    int nh = (ni >= 0 && ni < H && nj >= 0 && nj < W) ? A[ni][nj] : 0;
                    area += Math.Max(0, h - nh);
                }
            }
        }

        return area;
    }

}

class Solution
{
    public static void Main(string[] args)
    {
        TextWriter textWriter = new StreamWriter(@System.Environment.GetEnvironmentVariable("OUTPUT_PATH"), true);

        string[] HW = Console.ReadLine().TrimEnd().Split(' ');

        int H = Convert.ToInt32(HW[0]);

        int W = Convert.ToInt32(HW[1]);

        List<List<int>> A = new List<List<int>>();

        for (int i = 0; i < H; i++)
        {
            A.Add(Console.ReadLine().TrimEnd().Split(' ').ToList().Select(ATemp => Convert.ToInt32(ATemp)).ToList());
        }

        int result = Result.surfaceArea(A);

        textWriter.WriteLine(result);

        textWriter.Flush();
        textWriter.Close();
    }
}

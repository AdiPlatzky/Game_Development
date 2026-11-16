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
     * Complete the 'gridSearch' function below.
     *
     * The function is expected to return a STRING.
     * The function accepts following parameters:
     *  1. STRING_ARRAY G
     *  2. STRING_ARRAY P
     */

    public static string gridSearch(List<string> G, List<string> P)
    {
        int R = G.Count, C = G[0].Length;
        int r = P.Count, c = P[0].Length;

        for (int i = 0; i + r <= R; i++)
        {
            int j = G[i].IndexOf(P[0], 0, StringComparison.Ordinal);
            while (j != -1 && j + c <= C)
            {
                bool match = true;
                for (int k = 1; k < r && match; k++)
                {
                    if (string.CompareOrdinal(G[i + k], j, P[k], 0, c) != 0)
                        match = false;
                }

                if (match) return "YES";

                j = G[i].IndexOf(P[0], j + 1, StringComparison.Ordinal);
            }
        }

        return "NO";
    }

}

class Solution
{
    public static void Main(string[] args)
    {
        TextWriter textWriter = new StreamWriter(@System.Environment.GetEnvironmentVariable("OUTPUT_PATH"), true);

        int t = Convert.ToInt32(Console.ReadLine().Trim());

        for (int tItr = 0; tItr < t; tItr++)
        {
            int R = Convert.ToInt32(Console.ReadLine().TrimEnd().Split(' ')[0]);

            List<string> G = new List<string>();
            for (int i = 0; i < R; i++)
            {
                G.Add(Console.ReadLine().TrimEnd());
            }

            int r = Convert.ToInt32(Console.ReadLine().TrimEnd().Split(' ')[0]);

            List<string> P = new List<string>();
            for (int i = 0; i < r; i++)
            {
                P.Add(Console.ReadLine().TrimEnd());
            }

            string result = Result.gridSearch(G, P);

            textWriter.WriteLine(result);
        }

        textWriter.Flush();
        textWriter.Close();
    }
}

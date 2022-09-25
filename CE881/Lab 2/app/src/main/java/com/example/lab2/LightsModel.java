package com.example.lab2;

import java.util.Arrays;

public class LightsModel {

    int[][] grid;
    boolean notStrict = true;
    int n;


    public LightsModel(int n) {
        this.n = n;
        grid = new int[n][n];
    }

    public void tryFlip(int i, int j) {
        try {
            if (isSwitchOn(i, j) || notStrict) {
                flipLines(i, j);
            }
        } catch (Exception e) {
        }
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            sb.append(Arrays.toString(grid[i]) + "\n");
        }
        return sb.toString();
    }

    public boolean isSwitchOn(int i, int j) {
        // Check if the current switch is one
        return grid[i][j] == 1;

    }

    public void flipLines(int i, int j) {
        // Flip the whole row
        for (int x = 0; x < n; x++) {
            if (grid[i][x] == 1) {
                grid[i][x] = 0;
            } else {
                grid[i][x] = 1;
            }
        }

        // Flip the whole column
        for (int x = 0; x < n; x++) {
            if (grid[x][j] == 1) {
                grid[x][j] = 0;
            } else {
                grid[x][j] = 1;
            }
        }

        // Re-flip the initial panel as it would have flipped
        // twice back to its original state
        if (grid[i][j] == 1) {
            grid[i][j] = 0;
        } else {
            grid[i][j] = 1;
        }


    }

    public int getScore() {
        int counter = 0;
        for (int i = 0; i < n; i++) {
            for (int x = 0; x < n; x++) {
                if (grid[i][x] == 1) {
                    counter += 1;
                }
            }
        }
        return counter;
    }

    public boolean isSolved() {
        // Check if the game has been solved
        for (int i = 0; i < n; i++) {
            for (int x = 0; x < n; x++) {
                if (grid[i][x] == 0) {
                    return false;
                }
            }
        }
        return true;
    }

    public void reset() {
        for (int i = 0; i < n; i++) {
            for (int x = 0; x < n; x++) {
                if (grid[i][x] == 1) {
                    grid[i][x] = 0;
                }
            }
        }
    }
}


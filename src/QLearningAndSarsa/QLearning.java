import java.util.ArrayList;

public class QLearning
{

    private static MouseAndCheese mouseAndCheese;
    private static double alpha, gamma, epsilon;
    private static int initialPosition, cheesePosition;
    private static double[][] qStatesAndActions;

    public QLearning(double alpha, double gamma, double epsilon, int gridSize, int mouseLocation, int cheeseLocation)
    {
        mouseAndCheese = new MouseAndCheese(mouseLocation, cheeseLocation, gridSize);
        initialPosition = mouseLocation;
        this.cheesePosition = cheeseLocation;
        this.alpha = alpha;
        this.gamma = gamma;
        this.epsilon = epsilon;

        qStatesAndActions = new double[gridSize * gridSize][4];
    }

    public void startQLearn(int plays)
    {
        for(int play = 0; play < plays; play++)
        {
            while(!mouseAndCheese.isMouseOnCheese())
            {
                int startMouseState = mouseAndCheese.getMousePosition();
                int direction = 0;

                if(Math.random() > epsilon)
                {
                    double[] currentQValues = qStatesAndActions[startMouseState];
                    direction = getIndexOfLargestValueFromArray(currentQValues);
                }
                else
                {
                    direction = (int)(Math.random() * 4);
                }
                //System.out.println(startMouseState + " direction: " + direction);

                int reward = mouseAndCheese.getEnvironmentResponse(direction);

                double[] nextQValues = qStatesAndActions[mouseAndCheese.getMousePosition()];
                double maxQValue = getIndexOfLargestValueFromArray(nextQValues);

                qStatesAndActions[startMouseState][direction] = qStatesAndActions[startMouseState][direction] +
                        alpha * (reward + gamma * maxQValue - qStatesAndActions[startMouseState][direction]);

                //displayQStates();

            }
            mouseAndCheese.restart();

        }
        displayQStates();
        displayDirectionFromQStates();
    }

    public double getValueofLargestValueFromArray(double[] array)
    {
        double maxValue = 0.0;

        for(int i = 0; i < array.length; i++)
            if(array[i] > maxValue)
                maxValue = array[i];

        return maxValue;
    }
    public int getIndexOfLargestValueFromArray(double[] array)
    {
        double maxValue = Integer.MIN_VALUE;
        int maxIndex = 0;

        for(int i = 0; i < array.length; i++)
        {
            if(array[i] > maxValue)
            {
                maxValue = array[i];
                maxIndex = i;
            }
        }

        return maxIndex;
    }

    public void displayQStates()
    {
        for(double[] a : qStatesAndActions)
        {
            for(double x : a)
                System.out.print(x + " ");
            System.out.println();
        }
        System.out.println();
    }

    public void displayDirectionFromQStates()
    {

    }
}

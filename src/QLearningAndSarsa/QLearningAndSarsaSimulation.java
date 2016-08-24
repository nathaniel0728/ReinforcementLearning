public class QLearningAndSarsaSimulation
{
    public static void main(String[] args)
    {
        QLearning qLearning = new QLearning(0.5, 0.8, 0.1, 3, 0, 7);
        qLearning.startQLearn(200000);
    }
}

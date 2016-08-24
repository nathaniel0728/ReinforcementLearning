public class MouseAndCheese
{
    public static int initialPosition;
    public static int mousePosition, cheesePosition;
    public static int size;

    public MouseAndCheese(int mousePosition, int cheesePosition, int size)
    {
        this.initialPosition = mousePosition;
        this.mousePosition = mousePosition;
        this.cheesePosition = cheesePosition;
        this.size = size;
    }

    public int getEnvironmentResponse(int direction)
    {

        if(direction == 0) //north
        {
            if(mousePosition/size == 0) {
                //restartMousePosition();
                return -10;
            }
            else
            {
                mousePosition -= size;
                if(mousePosition == cheesePosition)
                    return 50;
                else
                    return 0;
            }
        }
        else if(direction == 1) //east
        {
            if(mousePosition % size == size - 1){
                //restartMousePosition();
                return -10;
            }
            else
            {
                mousePosition += 1;
                if(mousePosition == cheesePosition)
                    return 50;
                else
                    return 0;
            }
        }
        else if(direction == 2) //south
        {
            if(mousePosition / size == size - 1){
                //restartMousePosition();
                return -10;
            }
            else
            {
                mousePosition += size;
                if(mousePosition == cheesePosition)
                    return 50;
                else
                    return 0;
            }
        }
        else //west
        {
            if(mousePosition % size == 0){
                //restartMousePosition();
                return -10;
            }
            else
            {
                mousePosition -= 1;
                if(mousePosition == cheesePosition)
                    return 50;
                else
                    return 0;
            }
        }
    }

    public void restartMousePosition()
    {
        mousePosition = initialPosition;
    }
    public int getMousePosition()
    {
        return mousePosition;
    }
    public int getCheesePosition()
    {
        return cheesePosition;
    }
    public boolean isMouseOnCheese()
    {
        return mousePosition == cheesePosition;
    }
    public void restart()
    {
        mousePosition = initialPosition;
    }

}
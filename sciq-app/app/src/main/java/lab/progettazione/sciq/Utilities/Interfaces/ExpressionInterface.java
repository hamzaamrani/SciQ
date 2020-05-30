package lab.progettazione.sciq.Utilities.Interfaces;

import lab.progettazione.sciq.Model.Expression;

public interface ExpressionInterface {
    void onExpressionSuccessful(Expression expression);

    void onExpressionFailure(String error);
}

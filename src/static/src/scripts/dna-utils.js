String.prototype.format = function()
{
    return this.replace(/{(\d+)}/g, (match, number) => typeof arguments[number] != "undefined" ? arguments[number] : match);
}

Math.lerp = function(a, b, t)
{
    return a + (b - a) * t;
}

Math.ease_in = function(x)
{
    x = (x < 1) ? x : 1;
    x = (x > 0) ? x : 0;

    return 1 - Math.sqrt(1 - Math.pow(x, 2));
}

Math.ease_out = function(x)
{
    x = (x < 1) ? x : 1;
    x = (x > 0) ? x : 0;

    return Math.sqrt(1 - (1 - Math.pow(x, 2)));
}